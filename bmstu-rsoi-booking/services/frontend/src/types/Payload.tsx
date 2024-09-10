export interface Payload{
    jti: string,
	username: string,
	role: string,
	first_name?: string,
	last_name?: string,
	patronymic?: string,
	phone_number?: string,
	email?: string
}