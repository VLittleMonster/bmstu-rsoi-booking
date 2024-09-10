import React, { useState, useContext } from 'react';
import DatePicker from 'react-datepicker';
import "react-datepicker/src/stylesheets/datepicker.scss";
import { InputProps as IProps } from "@chakra-ui/react";

import ru from 'date-fns/locale/ru';
//import styles from './DateInputBox.module.scss';
import { DateContext } from 'components/DateInput/DateInput';


interface DateProps extends IProps {
    setStartDate?: CallableFunction,
    setEndDate?: CallableFunction
}

const DateInputBox: React.FC<DateProps> = (props) => {
    const [start, setStart] = useState(null);
    const [end, setEnd] = useState(null);
    
    const { setStartDate, setEndDate } = useContext(DateContext)!;

    const onChange = (dates) => {
        const [start, end] = dates;
        setStartDate(start);
        setEndDate(end);
        
        setStart(start);
        setEnd(end);

        if (start > end) {  // ЕСЛИ ДАТА НАЧАЛА БРОНИРОВАНИЯ > ДАТЫ ОКОНЧАНИЯ БРОНИ, ТО НАДО УВЕДОМИТЬ ЮЗЕРА

        }
    };

    return (
        <>
        <DatePicker 
            borderWidth='1px'
            borderColor='teal'
            selected={start}
            onChange={onChange}
            selectsRange
            minDate={new Date()}
            locale={ru}
            startDate={start}
            endDate={end}
            dateFormat="dd/MM/yyyy"
        />
        </>
    );
}

export default DateInputBox;