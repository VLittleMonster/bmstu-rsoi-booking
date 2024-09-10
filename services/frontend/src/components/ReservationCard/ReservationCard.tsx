import { Box, HStack, Image, Text, VStack, Badge, Center, Button } from "@chakra-ui/react";
import React from "react";

import { Reservation as ReservationI } from "types/Reservation";

import FullLikeBox from "components/Boxes/FullLike";

//import styles from "./ReservationCard.module.scss";
import GetImageUrl from "postAPI/likes/Get";
import CancelReservation from "postAPI/likes/Cancel";
import { statusItems } from "./items";


interface UserInfoProps extends ReservationI {}

const ReservationCard: React.FC<UserInfoProps> = (props) => {
  const [imageUrl, setImageUrl] = React.useState("https://media.discordapp.net/attachments/791290400086032437/1112498073478889502/default-fallback-image.png?width=720&height=480");
  const [status, setStatus] = React.useState(statusItems[props.status]);

  async function getImageUrl() {
    var data = await GetImageUrl(props.hotel.hotelUid);
    if (data.status === 200) {
      setImageUrl(data.content);
    }
  }

  async function submit(e: React.MouseEvent<HTMLButtonElement, MouseEvent>) {
    await CancelReservation(props.reservationUid);
    setStatus(statusItems['CANCELED']);
  }

  getImageUrl();

  return (
      <Box mt='4' p='4' bg='#40E0D0' borderWidth='1px' borderColor='teal' borderRadius='10'>
        <VStack>
        <Badge mt='2' fontFamily='Agency FB' borderRadius='full' px='65' colorScheme='teal' fontSize='3xl' width='100%'>
            <Center>{props.hotel.name}</Center>
        </Badge>

        <Box>
            <Text fontFamily='Century Gothic' color='gray.500'>{props.hotel.fullAddress}</Text>
        </Box>
        <Box px='2' borderWidth='1px' borderColor='teal' borderRadius='15' width='100%'>
            <Center><Text fontFamily='Century Gothic'>ЗАЕЗД: {props.startDate}</Text></Center>
        </Box>
        <Box px='2' borderWidth='1px' borderColor='teal' borderRadius='15' width='100%'>
            <Center><Text fontFamily='Century Gothic'>ВЫЕЗД: {props.endDate}</Text></Center>
        </Box>
        { status === 'Оплачено' && 
        <Box>
            <Text fontFamily='Century Gothic'>СТАТУС: { status }</Text>
        </Box> }
        { status === 'Отменено' && 
        <Box>
            <Text fontFamily='Century Gothic'>СТАТУС: { status }</Text>
        </Box> }

        <HStack>
            <FullLikeBox price={props.payment.price} />
        </HStack>
        </VStack>

        { (status === 'Оплачено') && 
            <Center>
            <Button colorScheme='teal' fontFamily='Century Gothic' type="submit" onClick={event => submit(event)}>
                Отменить Бронирование
            </Button> 
            </Center>
        }
    </Box>
  );
};

export default ReservationCard;
