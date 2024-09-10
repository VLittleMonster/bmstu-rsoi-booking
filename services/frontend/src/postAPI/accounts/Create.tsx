import { RegistrationCard } from "types/RegistrationCard";
import axiosBackend from "..";

interface resp {
    status: number
}

export const Create = async function(data: RegistrationCard): Promise<resp> {
    const response = await axiosBackend
        .post(`/register`, data)
        .catch((error) => {
            return {
                status: error.response?.status,
            };
    });

    return {
        status: response?.status,
    };
}
