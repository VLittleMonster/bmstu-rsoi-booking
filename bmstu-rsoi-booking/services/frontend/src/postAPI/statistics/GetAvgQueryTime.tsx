import axiosBackend from ".."
import { AllAvgQueryTimeResp } from "..";

const GetAvgQueryTime = async function(): Promise<AllAvgQueryTimeResp> {
    const response = await axiosBackend
        .get("/statistic/queries/avg-time");
    return {
        status: response.status,
        content: response.data
    };
}

export default GetAvgQueryTime
