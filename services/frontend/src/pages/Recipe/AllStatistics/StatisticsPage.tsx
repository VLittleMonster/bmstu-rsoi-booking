import { Box } from "@chakra-ui/react";
import React from "react";

//import styles from "./StatisticsPage.module.scss";
import GetAvgServiceTime from "postAPI/statistics/GetAvgServiceTime";
import StatisticsMap from "components/StatisticsMap/StatisticsMap";
import GetAvgQueryTime from "postAPI/statistics/GetAvgQueryTime";
import GetAllStatistic from "postAPI/statistics/GetAllStatistic";

interface StatisticsProps {}

const StatisticsPage: React.FC<StatisticsProps> = () => {
  return (
    <Box /*className={styles.main_box}*/>
      <StatisticsMap getCall={GetAvgServiceTime} getCallQuery={GetAvgQueryTime} getCallStatisticAll={GetAllStatistic} />
    </Box>
  );
};

export default StatisticsPage;
