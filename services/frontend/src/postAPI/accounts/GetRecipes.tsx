import axios from "axios";
import { AllHotelResp, backUrl } from "..";

const GetRecipes = async function(login: string): Promise<AllHotelResp> {
    const response = await axios.get(backUrl + `/accounts/${login}/recipes`);
    return {
        status: response.status,
        content: response.data
    };
}

export default GetRecipes