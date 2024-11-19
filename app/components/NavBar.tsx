import { Button } from "@nextui-org/button";
import { useState } from "react";
import { FaMoon } from "react-icons/fa6";
import { IoSunny } from "react-icons/io5";

export default function NavBar() {
    const [dark, setDark] = useState(false);
    const darkModeHandler = () => {
        setDark(!dark);
        document.body.classList.toggle('dark');
    }
    
    return (
        <div className="flex items-center justify-between mx-5 py-3">
            <div className="flex items-center gap-2">
                <div className="size-8 bg-slate-950 dark:bg-white rounded-md"></div>
                <h1 className="text-2xl font-semibold">QueryForge</h1>
            </div>
            <div>
                <Button isIconOnly size="md" variant="flat" onClick={darkModeHandler}>
                  {dark ? (<IoSunny className="w-5 h-5" />) : (<FaMoon className="w-5 h-5" />)}
                </Button> 
            </div>
        </div>
    )
}