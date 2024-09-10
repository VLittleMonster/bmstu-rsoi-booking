import { Hotel } from "./Hotel";

export interface HotelResponse {
	page:           number,
	pageSize:       number,
	totalElements:  number,
	items:  		Hotel[]
}