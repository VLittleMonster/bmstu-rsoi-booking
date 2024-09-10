import { Box, Container, Text, HStack, Center} from "@chakra-ui/react";
import React from "react";
import { AvgQueryServiceTime as AvgQueryServiceTimeI } from "types/AvgQueryServiceTime";

//import styles from "./StatisticsAvgQueryTimeCard.module.scss";

interface StatisticsAvgQueryTimeProps extends AvgQueryServiceTimeI {}


const StatisticsAvgQueryTimeCard: React.FC<StatisticsAvgQueryTimeProps> = (props) => {
    return (
        <Box /*className={styles.main_box}*/>
            <Center>
            <Box py='2' mb='4' bg='#40E0D0' borderRadius='15' width='95%'>
                <Container>
                    <Text fontSize='xl' as='i'>{props.eventAction}</Text>

                    <HStack>
                    <Text color='gray.500'>Сервис:</Text>
                    <Text>{props.serviceName}</Text>
                    </HStack>

                    <HStack>
                    <Text color='gray.500' mr='46'>Количество запросов:</Text>
                    <Text>{props.num}</Text>
                    </HStack>

                    <HStack>
                    <Text color='gray.500'>Среднее время обработки:</Text>
                    <Text>{props.avgTime.toFixed(3)} мс</Text>
                    </HStack>
                
                </Container>
            </Box>
            </Center>
        </Box>
    )
};

export default StatisticsAvgQueryTimeCard;