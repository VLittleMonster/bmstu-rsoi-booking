import axiosBackend from ".."
import { AllHotelResp } from "..";

const GetHotels = async function(): Promise<AllHotelResp> {
    const params = { page: 1, size: 50 }
    const response = await axiosBackend.get("/hotels", {params:params});

    return {
        status: response.status,
        content: response.data
    };
}

export default GetHotels
