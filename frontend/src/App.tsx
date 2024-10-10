import './App.scss'
import {Link} from "@trussworks/react-uswds";
import {useLocation} from "react-router-dom";

import {AppHeader} from "./components/AppHeader/AppHeader.tsx";

import {TemplatesIndex} from "./components/TemplatesIndex/TemplatesIndex.tsx";
function App() {
    const {pathname} = useLocation()
    const navLinks = [
        {text: "Annotate and Extract", url: "/"},
        {text: "Label Management", url: "/labels"},
        {text: "Dashboard", url: "/dashboard"}
    ]

    return (
        <>
            <div className='display-flex flex-column width-full height-full'>
                <AppHeader jurisdiction={`Demo STLT`}/>
                <div className="display-flex flex-row height-full">
                    <div
                        className="flex-3 padding-top-1 padding-left-1 padding-right-4 minw-15 usa-dark-background bg-primary-dark text-base-lightest display-flex flex-column flex-gap-1 maxw-30 side-nav"
                        >
                        <div className='display-flex flex-column flex-align-start padding-top-2'>
                            {navLinks.map((i, idx) => {
                                return <Link key={idx} href={i.url}
                                             className={`border-left-2px padding-left-1 padding-top-2 padding-bottom-2 nav-link ${i.url === pathname ? 'text-bold' : 'border-primary-dark'}`}>{i.text}</Link>
                            })}
                        </div>
                    </div>

                    <div className="flex-10 display-flex flex-column">
                        <h2 className="padding-left-2">Annotate and Extract</h2>
                        <div className=" flex-1 padding-left-2  padding-right-2 bg-idwa-light">
                            <p><span className="text-bold">Welcome Blake, </span></p>
                            <p>Extract data from any PDFs, or images to send to your surveillance systems using data
                                from your saved templates or create new segmentations.</p>
                            <TemplatesIndex/>
                        </div>
                    </div>
                </div>

            </div>

        </>
    )
}

export default App
