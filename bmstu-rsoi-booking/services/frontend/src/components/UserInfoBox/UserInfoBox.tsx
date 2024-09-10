import { Box, VStack, HStack, Text, Container, Center} from "@chakra-ui/react";
import React from "react";
import { UserInfoResp } from "postAPI";

//import styles from "./ReservationMap.module.scss";
import ReservationCard from "components/ReservationCard/ReservationCard";
import { Reservation } from "types/Reservation";
import { UserInfo } from "types/UserInfo";
import { LoyaltyInfo } from "types/LoyaltyInfo";

interface UserInfoBoxProps {
    searchQuery?: string
    getCall: (title?: string) => Promise<UserInfoResp>
}

type State = {
    profile?: any
    reservations?: any
    loyalty?: any
}

class UserInfoBox extends React.Component<UserInfoBoxProps, State> {
    constructor(props) {
        super(props);
        this.state = {
            profile: {},
            reservations: [],
            loyalty: {}
        }
    }

    async getAll() {
        var data = await this.props.getCall(this.props.searchQuery)
        if (data.status === 200)
            this.setState({
                profile: data.content.profile,
                reservations: data.content.reservations,
                loyalty: data.content.loyalty
            });
    }

    componentDidMount() {
        this.getAll()
    }

    componentDidUpdate(prevProps) {
        if (this.props.searchQuery !== prevProps.searchQuery) {
            this.getAll()
        }
    }

    render() {
        return (
            <Box fontFamily='Century Gothic' bg='#40E0D0' borderRadius='15' p='3'>

                <Center>
                <HStack pb='5'>
                <Text as='b' fontSize="2xl" color='gray.500'>ПРОФИЛЬ</Text>
                <Text fontSize="2xl" color='black'>{this.state.profile.name}</Text>
                </HStack>
                </Center>

                <HStack>
                
                <Container>
                
                <HStack>
                <Text color='gray.500'>Имя:</Text>
                <Text color='black'>{this.state.profile.name}</Text>
                </HStack>

                <HStack>
                <Text color='gray.500'>Фамилия:</Text>
                <Text color='black'>{this.state.profile.surname}</Text>
                </HStack>

                <HStack>
                <Text color='gray.500'>Отчество:</Text>
                <Text color='black'>{this.state.profile.patronymic}</Text>
                </HStack>

                </Container>

                <Container width='100%'>

                <HStack>
                <Text color='gray.500'>Телефон:</Text>
                <Text color='black'>{this.state.profile.phoneNumber}</Text>
                </HStack>

                <HStack>
                <Text color='gray.500'>Лояльность:</Text>
                <Text color='black'>{this.state.loyalty.status} {this.state.loyalty.discount}%</Text>
                </HStack>

                <HStack>
                <Text color='gray.500'>Бронирований:</Text>
                <Text color='black'>{this.state.loyalty.reservationCount}</Text>
                </HStack>

                </Container>

                </HStack>

                <Text>{this.state.reservations.map(item => <ReservationCard {...item} key={item.id}/>)}</Text>
            </Box>
        )
    }
}

export default React.memo(UserInfoBox);
