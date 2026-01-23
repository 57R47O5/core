import request from "../api/requests";
import { setToken, clearToken } from "./tokenService";

export const login = async (data) => {
   try {
    const response = await request.post("login/", data);
    setToken(response.token);
    return response;
  } catch (error) {
    throw error;
  }
};

export const logout = async () => {
  await request.post("logout/");
  clearToken();
};
export const register = (data) => request.post(`register/`, data);
export const me = ()=> request.get(`me/`)