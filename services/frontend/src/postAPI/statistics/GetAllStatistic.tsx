import axiosBackend from ".."
import { AllStatisticResp } from "..";

const GetAllStatistic = async function(): Promise<AllStatisticResp> {
    const response = await axiosBackend
        .get("/statistic/all");
    return {
        status: response.status,
        content: response.data
    };
}

export default GetAllStatistic
