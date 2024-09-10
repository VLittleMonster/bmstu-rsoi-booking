import axiosBackend from "..";

interface resp {
    status: number
}

const CancelReservation = async function(reservationUid: number): Promise<resp> {
    const response = await axiosBackend
        .delete(`/reservations/${reservationUid}`);
    return {
        status: response.status,
    };
}
export default CancelReservation;