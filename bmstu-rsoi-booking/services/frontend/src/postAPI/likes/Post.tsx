import axiosBackend from "..";
import {ReservationRequest as ReservationRequestT} from "types/ReservationRequest"

interface resp {
    status: number
}

const PostReservation = async function(data: ReservationRequestT): Promise<resp> {
    const response = await axiosBackend
        .post(`/reservations`, data);
    return {
        status: response.status
    };
}
export default PostReservation;
