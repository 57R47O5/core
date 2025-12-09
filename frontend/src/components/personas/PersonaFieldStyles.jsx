export const fieldContainerStyle = {
  marginBottom: 15,
};

export const labelStyle = {
  display: "block",
  marginBottom: 5,
  fontWeight: 500,
};

export const inputStyle = (isReadOnly) => ({
  display: "block",
  width: "100%",
  padding: 6,
  borderRadius: 5,
  border: "1px solid #ccc",
  backgroundColor: isReadOnly ? "#f8f8f8" : "white",
});

export const errorStyle = {
  color: "red",
  marginTop: 5,
};
