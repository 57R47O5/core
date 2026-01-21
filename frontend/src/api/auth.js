import request from "../api/requests";

BASE_URL = "auth/"

export const register = (data) => request.post(`${BASE_URL}register/`, data);
export const login = (data) => request.post(`${BASE_URL}login/`, data);
export const logout = (data) => request.post(`${BASE_URL}logout/`, data);
export const me = ()=> request.get(`${BASE_URL}me/`)