import { Console, log } from "console";
import axiosBackend from ".."
import { Account } from "types/Account";

interface resp {
  status: number
}

export const Login = async function (data: Account): Promise<resp> {
  const response = await axiosBackend
    .post(`/oauth/token`, data)
    .then((data) => data)
    .catch((error) => {
      return { status: error.response?.status, data: error.response?.data };
    });
  return {
    status: response?.status,
  };
};
