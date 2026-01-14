import request from "@/api/requests";

export const login = async (credentials) => {
  return await request.post("/auth/login/", credentials);
};

export const logout = async () => {
  return await request.post("/auth/logout/");
};

export const getSession = async () => {
  return await request.get("/auth/session/");
};
