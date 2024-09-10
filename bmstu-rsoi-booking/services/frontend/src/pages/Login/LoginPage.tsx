import React from "react";

import { Box, Link, Input, Button, Text, Center } from "@chakra-ui/react";
import { NavigateFunction } from "react-router-dom";

// import Input from "components/Input";
// import RoundButton from "components/RoundButton";

import { Account } from "types/Account"
import { Login as LoginQuery } from "postAPI/accounts/Login";

//import styles from "./LoginPage.module.scss";

type LoginProps = {
    navigate: NavigateFunction
}


class LoginPage extends React.Component<LoginProps> {
    acc: Account = {scope: "openid profile", grant_type: "password", username: "", password: ""}

    setLogin(val: string) {
        this.acc.username = val
    }
    setPassword(val: string) {
        this.acc.password = val
    }

    submit(e: React.MouseEvent<HTMLButtonElement, MouseEvent>) {
        var temp = e.currentTarget
        temp.disabled = true
        LoginQuery(this.acc).then(data => {
            temp.disabled = false

            if (data.status === 200) {
                window.location.href = '/';
            } else {
                var title = document.getElementById("undertitle")
                if (title)
                    title.innerText = "Ошибка авторизации!"
            }
        });
    }

    render() {
        return <Box fontFamily='Century Gothic' bg='#40E0D0' borderRadius='10' width='50%'>
            <Box p='3'>
                <Center>
                <Text fontSize='2xl'>Авторизация</Text>
                </Center>
            </Box>
            
            <Box p='3'>
            <Center>
                <Input width='95%' variant='filled' name="login" type="login" placeholder="Логин"
                onInput={event => this.setLogin(event.currentTarget.value)}/>
            </Center>
            </Box>
            <Box p='3'>
            <Center>
                <Input width='95%' variant='filled' name="password" type="password" placeholder="Пароль"
                onInput={event => this.setPassword(event.currentTarget.value)}/>
                </Center>
            </Box>

            <Box p='3'>
                <Box>
                    <Center>
                    <Button width='95%' colorScheme='teal' onClick={ (event) => this.submit(event) }> Войти </Button>
                    </Center>
                </Box>

                <Box>
                    <Text mt='4' ml='4'>Еще нет аккаунта?    
                        <Link color='teal.500' href="/register"> Зарегистрироваться </Link>
                    </Text>
                </Box>
                <Box>
                    <Link ml='4' color='teal.500' href="/">Назад</Link>
                </Box>
            </Box>
        </Box>
    }
}

export default LoginPage;
