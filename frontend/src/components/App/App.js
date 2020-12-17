import './App.css';
import '../Navbar/Navbar'
import Navbar from '../Navbar/Navbar';
import { Route, Switch, BrowserRouter} from "react-router-dom";

function App() {
  return (
    <div className="App">
        <BrowserRouter>
            <Switch>
                <Route
                    path="/"
                    component={Navbar}
                    exact={true}
                />
            </Switch>
        </BrowserRouter>
    </div>
  );
}

export default App;
