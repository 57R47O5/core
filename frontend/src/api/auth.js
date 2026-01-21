import request from "../api/requests";

export const register = (data) => request.post(`register/`, data);
export const login = (data) => request.post(`login/`, data);
export const logout = (data) => request.post(`logout/`, data);
export const check = ()=> request.get(`check-auth/`)