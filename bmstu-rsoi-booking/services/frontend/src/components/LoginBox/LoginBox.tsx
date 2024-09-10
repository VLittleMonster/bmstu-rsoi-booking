import React from "react";
import {
    InputProps as IProps,
    Box, Text
} from "@chakra-ui/react";
// import Settings from "components/Icons/Settings";

//import styles from "./LoginBox.module.scss";

interface InputProps extends IProps {
    login?: number | string
}

const LoginBox: React.FC<InputProps> = (props) => {
    return (
    <Box> 
        {/* <Box> <Settings /> </Box> */}
        <Text> {props.login} </Text>
    </Box>
    )
}

export default LoginBox;