import { Box } from "@chakra-ui/react";
import GetUserInfo from "postAPI/likes/GetUserInfo";
import React from "react";

//import styles from "./ReservationsPage.module.scss";
import UserInfoBox from "components/UserInfoBox/UserInfoBox";

interface UserInfoProps {}

const UserInfoPage: React.FC<UserInfoProps> = () => {
  return (
    <Box width='50%'>
      <UserInfoBox getCall={GetUserInfo} />
    </Box>
  );
};

export default UserInfoPage;
