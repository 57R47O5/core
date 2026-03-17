export const resolveValidationSchema = ({
  formModel,
  FormComponent={},
  context,
}) => {
  const baseSchema = formModel.baseValidationSchema;

  const contextSchema =
    FormComponent.getContextValidationSchema?.(context);

  if (!contextSchema) return baseSchema;

  return baseSchema.concat(contextSchema);
};