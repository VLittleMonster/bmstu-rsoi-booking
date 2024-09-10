import { HotelInfo } from "./HotelInfo";
import { PaymentInfo } from "./PaymentInfo";

export interface Reservation {
	reservationUid:             number,
    hotel:                      HotelInfo,
    startDate:                  Date,
    endDate:                    Date,
    status:                     string,
    payment:                    PaymentInfo
}