import axiosBackend from ".."
import { AllAvgServiceTimeResp } from "..";

const GetAvgServiceTime = async function(): Promise<AllAvgServiceTimeResp> {
    const response = await axiosBackend
        .get("/statistic/services/avg-time");
    return {
        status: response.status,
        content: response.data
    };
}

export default GetAvgServiceTime
