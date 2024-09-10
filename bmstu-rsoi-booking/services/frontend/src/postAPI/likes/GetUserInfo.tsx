import axiosBackend from ".."
import { UserInfoResp } from "..";

const GetUserInfo = async function(): Promise<UserInfoResp> {
    const response = await axiosBackend
        .get(`/me`);
    console.log("userinfo: ", response.status, "\n", response.data);
    return {
        status: response.status,
        content: response.data
    };
}

export default GetUserInfo