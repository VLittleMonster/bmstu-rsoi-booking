import { UserInfoResp } from "postAPI";
import { Reservation } from "./Reservation";
import { LoyaltyInfo } from "./LoyaltyInfo";


export interface UserInfo {
	profile: UserInfoResp,
	reservations: Reservation[],
	loyalty: LoyaltyInfo
}