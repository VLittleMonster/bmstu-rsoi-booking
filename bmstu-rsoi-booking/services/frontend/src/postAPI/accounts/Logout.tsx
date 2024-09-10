import axiosBackend from "postAPI/index";
import { backUrl } from "..";

export const Logout = async function() {
    const response = await axiosBackend.post(backUrl + `/oauth/revoke`).catch((error) => {
        return {
            status: error.response?.status,
        };
    });

    localStorage.clear()
    window.location.href = '/authorize';
    return response;
}
