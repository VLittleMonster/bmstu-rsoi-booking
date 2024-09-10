import React from "react";
import {
  Box,
  Container, HStack, Center, VStack
} from "@chakra-ui/react";

//import styles from "./Header.module.scss";

import Navbar from "./Navbar"
import Titles, { TitlesProps } from "components/Header/Titles/Titles";

export interface HeaderProps extends TitlesProps {
    role?: string
    addField?: JSX.Element
}

const Header: React.FC<HeaderProps> = (props) => {
    return (
    <Box>
    <Center>
    <Box bg='#40E0D0' borderRadius='full' width='80%' mt='3' py='2'>
    <Center>
            <Navbar />
    </Center>
    </Box>
    </Center>
    <Center mt='5'>
    <Titles {...props}/>
    {props.addField && props.addField}
    </Center>
    </Box>
    );
}

export default React.memo(Header);
