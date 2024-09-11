// import { Category } from "types/Categories";
import { Account } from "types/Account";
import axios from "axios";
import { HotelResponse } from "types/HotelResponse";
//import { Reservation } from "types/Reservation";
import { UserInfo } from "types/UserInfo";
import { AvgServiceTime } from "types/AvgServiceTime";
import { AvgQueryServiceTime } from "types/AvgQueryServiceTime";
import { Payload } from "types/Payload";
import {jwtDecode} from "jwt-decode";
import { StatisticEventInfo } from "types/StatisticEventInfo";

export const backUrl = "http://84.201.148.115/booking-service/api/v1";

const axiosBackend = () => {
    let instance = axios.create({
        baseURL: backUrl,
        withCredentials: true
    });

    instance.interceptors.request.use(function (config) {
        if (config.url?.includes("/oauth/token") || config.url?.includes("/oauth/revoke")){
            const refresh_token = localStorage.getItem("refresh_token");
            if (config.headers && refresh_token) {
                config.headers.Authorization = 'Bearer ' + refresh_token;
            }
        }
        else {
            const token = localStorage.getItem("token");
            if (config.headers && token) {
                config.headers.Authorization = 'Bearer ' + token;
            }
        }

        return config;
    })

    instance.interceptors.response.use(async function (response) {
        if (response.config.url?.includes("/register") || 
            response.config.url?.includes("/oauth/token")) {
                if (response.status === 200) {
                    localStorage.setItem("token", response.data.access_token);
                    localStorage.setItem("refresh_token", response.data.refresh_token);
                    localStorage.setItem("scope", response.data.scope);
                    localStorage.setItem("expires_in", response.data.expires_in);

                    const payload = jwtDecode<Payload>(response.data.access_token);
                    localStorage.setItem("role", payload.role);
                    localStorage.setItem("username", payload.username);
                }
            }
        return response;
    }, 
    async function (error) {
        if (error.config.url?.includes("/register") || 
            error.config.url?.includes("/oauth/token")){
            if (error.response.status === 401) {
                localStorage.clear()
                if (!window.location.href.includes('/authorize'))
                    window.location.href = '/authorize';
            }
        } else {
            if (error.response.status === 401) {
                console.log("try to refresh tokens");
                const refreshTokenRequest: Account = {
                    scope: "openid profile", 
                    grant_type: "refresh-token", 
                    username: "",
                    password: ""
                };
                const refreshTokenResponse = await instance.post("/oauth/token", refreshTokenRequest)
                        .then((data) => data)
                        .catch((error) => {
                            return { status: error.response?.status, data: error.response?.data };
                        });
                
                if (refreshTokenResponse.status === 200){
                    return await instance.request(error.config);
                }
            }
        }
        return error;
    });

    return instance;
}

export default axiosBackend();


export type AllHotelResp = {
    status: number,
    content: HotelResponse
}

export type UserInfoResp = {
    status: number,
    content: UserInfo
}

export type AllAvgServiceTimeResp = {
    status: number,
    content: AvgServiceTime[]
}

export type AllAvgQueryTimeResp = {
    status: number,
    content: AvgQueryServiceTime[]
}

export type AllStatisticResp = {
    status: number,
    content: StatisticEventInfo[]
}

export type AllUsersResp = {
    status: number,
    content: Account[]
}
