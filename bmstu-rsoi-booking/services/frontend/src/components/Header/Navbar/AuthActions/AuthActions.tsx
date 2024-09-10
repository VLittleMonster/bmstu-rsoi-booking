import React from "react";
import { Box, Text, Link, HStack } from "@chakra-ui/react";

import AuthorIcon from "components/Icons/Author";
import { Logout } from "postAPI/accounts/Logout";

export interface AuthActionsProps {
    login: string
}
const AuthActions: React.FC<AuthActionsProps> = (props) => {
    let role = (localStorage.getItem("role") !== null ? localStorage.getItem('role') : '')!;

    return (
        <Box fontFamily='Century Gothic' fontSize='xl'> 
            <HStack>
            <Text as='b'>{props.login}</Text>
            <AuthorIcon/>
            <Link pl='4' href="/me">ПРОФИЛЬ</Link>
            <Link pl='4' href="/">ОТЕЛИ</Link>
            {role === 'admin' && <Link pl='4' href="/statistics">СТАТИСТИКА</Link>}
            <Link pl='4' onClick={Logout}>ВЫЙТИ</Link>
            </HStack>
        </Box>
    )
}

export default React.memo(AuthActions);
