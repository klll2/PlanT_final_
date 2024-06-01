import React from 'react';
import {
    Container,
    Row,
    Col,
} from "reactstrap";
import { GoogleOAuthProvider, GoogleLogin } from '@react-oauth/google';
import axios from 'axios';
import { jwtDecode } from "jwt-decode";
// import { useCookies } from 'react-cookie';


const GoogleLoginButton = () => {
    // const [cookies, setCookie] = useCookies(['trvlr_id', 'trvlr_email']);

    const handleLoginSuccess = async (response) => {
        try {
            console.log(response);       
            var profileObj = jwtDecode(response.credential);
            console.log(profileObj);
            const mail = JSON.stringify(profileObj.email);
            const djangoResponse = await axios.post('http://localhost:8000/account/login/', { mail });
            console.log(djangoResponse.data); // Django로부터 받은 사용자 정보 출력
            const { id, email } = djangoResponse.data;
            localStorage.setItem("trvlr_id", id);
            console.log('User created:', djangoResponse.data);
            window.location.href = 'http://localhost:3000/admin/mypage/';

        } catch (error) {
            console.error(error);
        }
    };

    const handleLoginFailure = (error) => {
        console.error(error);
    };

    return (
        <Container>
            <Row className="justify-content-center">
                <Col xs="auto">
                    <GoogleOAuthProvider clientId="564324845555-4e3ovl5392l42f8fig3u8gc98vg7j8rm.apps.googleusercontent.com">
                        <GoogleLogin
                                onSuccess={handleLoginSuccess}
                                onFailure={handleLoginFailure}
                        />
                    </GoogleOAuthProvider>
                </Col>
            </Row>
        </Container>
    );
};

export default GoogleLoginButton;