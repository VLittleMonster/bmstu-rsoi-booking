import React from "react";
import { Routes, Route } from "react-router";
import { BrowserRouter } from "react-router-dom";
import Header from ".";


export const HeaderRouter: React.FC<{}> = () => {
    return <BrowserRouter>
        <Routes>
            <Route path="/" element={<Header title="Все отели"/>}/>
            <Route path="/me/reservations" element={<Header subtitle="Бронирования" title="Мои" />}/>
            <Route path="/statistics" element={<Header subtitle="Общая" title="Статистика" />}/>
            <Route path="/authorize" element={<Header title="Вход" undertitle="" />}/>
            <Route path="/register" element={<Header title="Регистрация" undertitle="" />}/>

            <Route path="*" element={<Header title="Страница не найдена"/>}/>
        </Routes>
    </BrowserRouter>
}
