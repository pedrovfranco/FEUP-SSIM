import './App.css';
import { Route, Switch, BrowserRouter} from "react-router-dom";
import Navbar from '../Navbar/Navbar';
import Ranking from '../Ranking/Ranking'
import Rewards from '../Rewards/Rewards'

function App() {
  return (
    <div className="App">
        <BrowserRouter>
            <Switch>
                <Route
                    path="/"
                    component={Ranking}
                    exact={true}
                />
                <Route
                    path="/ranking"
                    component={Ranking}
                    exact={true}
                />
                <Route
                    path="/rewards"
                    component={Rewards}
                    exact={true}
                />
            </Switch>
        </BrowserRouter>
    </div>
  );
}

export default App;
