import axiosBackend from "..";

interface resp {
    status: number
    content: string
}

const GetImageUrl = async function(hotelUid: number): Promise<resp> {
    const response = await axiosBackend.get(`/hotels/${hotelUid}/image`);
    return {
        status: response.status,
        content: response.data as string
    };
}
export default GetImageUrl;
