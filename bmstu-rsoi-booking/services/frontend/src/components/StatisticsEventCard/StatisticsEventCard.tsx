import { Box, Container, Text, VStack, HStack, Center } from "@chakra-ui/react";
import React from "react";
import { StatisticEventInfo } from "types/StatisticEventInfo";

//import styles from "./PopularHotelCard.module.scss";

interface StatisticEventProps extends StatisticEventInfo {}

const StatisticsEventCard: React.FC<StatisticEventProps> = (props) => {
    return (
        <Box /*className={styles.main_box}*/>
            <Center>
            <Box py='2' mb='4' bg='#40E0D0' borderRadius='15' width='95%'>
                <Container>
                    <Text fontSize='xl' as='i'>{props.username}</Text>

                    <HStack>
                    <Text color='gray.500'>Сервис:</Text>
                    <Text>{props.serviceName}</Text>
                    </HStack>

                    <HStack>
                    <Text color='gray.500'>Запрос:</Text>
                    <Text>{props.eventAction}</Text>
                    </HStack>

                    <HStack>
                    <Text color='gray.500'>Время:</Text>
                    <Text>{props.startTime}</Text>
                    </HStack>
                
                </Container>
            </Box>
            </Center>
        </Box>
    );
}

export default StatisticsEventCard;