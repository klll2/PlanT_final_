import { BrowserRouter, Routes, Route } from "react-router-dom";
import MyForm from './testhello';


function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="" element={<MyForm />}></Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
