import { Box, Text, HStack, Center } from "@chakra-ui/react";
import React from "react";

//import styles from "./Statistics.module.scss";
import { AllAvgQueryTimeResp, AllAvgServiceTimeResp, AllStatisticResp } from "postAPI";
import StatisticsAvgServiceTimeCard from "components/StatisticsAvgServiceTimeCard/StatisticsAvgServiceTimeCard";
import StatisticsAvgQueryTimeCard from "components/StatisticsAvgQueryTimeCard/StatisticsAvgQueryTimeCard";
import StatisticsEventCard from "components/StatisticsEventCard/StatisticsEventCard";


interface StatisticsBoxProps {
    searchQuery?: string
    getCall: () => Promise<AllAvgServiceTimeResp>
    getCallQuery: () => Promise<AllAvgQueryTimeResp>
    getCallStatisticAll: () => Promise<AllStatisticResp>
}

type State = {
    avgServiceTime?: any
    avgQueryTime?: any
    allStatistic?: any
}


class StatisticsMap extends React.Component<StatisticsBoxProps, State> {
    constructor(props) {
        super(props);
        this.state = {
            avgServiceTime: [],
            avgQueryTime: [],
            allStatistic: []
        }
    }

    async getAllAvgServiceTime() {
        var data = await this.props.getCall();
        if (data.status === 200)
            this.setState({avgServiceTime: data.content})
    }

    async getAllAvgQueryTime() {
        var data = await this.props.getCallQuery();
        if (data.status === 200)
            this.setState({avgQueryTime: data.content})
    }

    async getAllStatistic() {
        var data = await this.props.getCallStatisticAll();
        if (data.status === 200)
            this.setState({allStatistic: data.content})
    }

    componentDidMount() {
        if (localStorage.getItem("role") !== "admin"){
            window.location.href = "/";
            return;
        }

        this.getAllAvgServiceTime();
        this.getAllAvgQueryTime();
        this.getAllStatistic();
    }

    render() {
        return (
            <Box fontFamily='Century Gothic' width='100%'>

                
                <Box borderRadius='15' borderWidth='2px' borderColor='teal'>
                <Center>
                <Text my='4' fontSize='2xl'>
                    ----------------------- СЕРВИСЫ ----------------------
                </Text>
                </Center>
                {this.state.avgServiceTime.map(item => <StatisticsAvgServiceTimeCard {...item} key={item.id}/>)}
                </Box>

                <Box mt='8' borderRadius='15' borderWidth='2px' borderColor='teal'>
                <Center>
                <Text my='4' fontSize='2xl'>
                    -------- ХАРАКТЕРИСТИКИ ПО ЗАПРОСАМ --------
                </Text>
                </Center>
                {this.state.avgQueryTime.map(item => <StatisticsAvgQueryTimeCard {...item} key={item.id}/>)}
                </Box>
                
                
                <Box mt='8' borderRadius='15' borderWidth='2px' borderColor='teal'>
                <Center>
                <Text my='4' fontSize='2xl'>
                    ---------------------- ЗАПРОСЫ -----------------------
                </Text>
                </Center>
                {this.state.allStatistic.map(item => <StatisticsEventCard {...item} key={item.id}/>)}
                </Box>
                
            </Box>
        )
    }
}

export default React.memo(StatisticsMap);