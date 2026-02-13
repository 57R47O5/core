from dataclasses import dataclass
from typing import Dict, Set, Literal


# ------------------------------------------------------------
# Core Concepts
# ------------------------------------------------------------

Action = Literal["create", "view", "update", "delete"]


@dataclass(frozen=True)
class ResourceDefinition:
    """
    Represents a domain resource (e.g. 'colaborador', 'votante').

    It defines which actions are structurally allowed on that resource.
    This is NOT a permission assignment. It only defines the capability surface.
    """
    name: str
    allowed_actions: Set[Action]


@dataclass(frozen=True)
class PermissionGrant:
    """
    Represents a single atomic permission.

    A permission is defined as:
        (resource_name, action)

    Example:
        PermissionGrant("colaborador", "view")
    """
    resource: str
    action: Action


@dataclass(frozen=True)
class RoleDefinition:
    """
    Represents a role within the application.

    A role is defined as:
        - A name
        - A set of atomic permission grants

    A role DOES NOT define resources.
    A role only aggregates existing permissions.
    """
    name: str
    permissions: Set[PermissionGrant]


@dataclass
class AppSecurityModel:
    """
    Represents the complete security structure of an application.

    It contains:
        - The resources that exist
        - The roles that grant permissions

    This model allows both structural validation and
    organizational analysis.
    """

    app_name: str
    resources: Dict[str, ResourceDefinition]
    roles: Dict[str, RoleDefinition]

    # ------------------------------------------------------------
    # Structural Validation
    # ------------------------------------------------------------

    def validate(self) -> None:
        """
        Validates that:

        1. Every permission grant references an existing resource.
        2. Every granted action is allowed by that resource.
        3. No role contains invalid or undefined permissions.

        Raises:
            ValueError if inconsistencies are found.
        """
        for role in self.roles.values():
            for permission in role.permissions:

                if permission.resource not in self.resources:
                    raise ValueError(
                        f"Role '{role.name}' references unknown resource "
                        f"'{permission.resource}'"
                    )

                resource = self.resources[permission.resource]

                if permission.action not in resource.allowed_actions:
                    raise ValueError(
                        f"Role '{role.name}' grants invalid action "
                        f"'{permission.action}' on resource "
                        f"'{permission.resource}'"
                    )

    # ------------------------------------------------------------
    # Organizational Analysis
    # ------------------------------------------------------------

    def permission_matrix(self) -> Dict[str, Set[PermissionGrant]]:
        """
        Returns a role → permissions mapping.

        Useful for:
            - Exporting to audit reports
            - Generating role-permission matrices
            - Comparing roles
        """
        return {
            role.name: role.permissions
            for role in self.roles.values()
        }

    def resource_coverage(self) -> Dict[str, int]:
        """
        Returns how many roles grant access to each resource.

        This helps identify:
            - Critical resources (widely accessible)
            - Isolated resources (rarely used)
        """
        coverage: Dict[str, int] = {
            resource_name: 0
            for resource_name in self.resources
        }

        for role in self.roles.values():
            granted_resources = {p.resource for p in role.permissions}
            for resource_name in granted_resources:
                coverage[resource_name] += 1

        return coverage

    def role_density(self) -> Dict[str, int]:
        """
        Returns the number of permissions granted by each role.

        Useful to detect:
            - Overpowered roles
            - Minimal roles
            - Structural imbalance
        """
        return {
            role.name: len(role.permissions)
            for role in self.roles.values()
        }
