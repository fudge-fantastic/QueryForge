import { Form } from "@remix-run/react";
import { useState } from "react";
import { Button, Input, Accordion, AccordionItem, Progress } from "@nextui-org/react";
import axios from "axios";
import Markdown from 'react-markdown';

const api = axios.create({
    baseURL: "http://localhost:8000"
});

export default function QuestionForm() {
    const [question, setQuestion] = useState("");
    const [answer, setAnswer] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const [documents, setDocuments] = useState([]);

    const handleSubmit = async (e: { preventDefault: () => void; }) => {
        setAnswer("");
        e.preventDefault();
        setIsLoading(true);
        console.log("Your Question: " + question);
        try {
            const response = await api.post("/ask_question", { message: question });
            setAnswer(response.data.answer);
            setDocuments(response.data.documents || []);
        } catch (error) {
            console.error("Error fetching answer:", error);
        }
        setIsLoading(false);
    };

    const handleIndexing = async (e: { preventDefault: () => void; }) => {
        setAnswer("");
        e.preventDefault();
        setIsLoading(true);
        console.log("Website URL Indexing");
    
        try {
            const response = await api.post("/index_website", { website_url: question });
            if (response.data.error) {
                console.error("Error indexing website:", response.data.error);
                setAnswer("Failed to index website. Please try again.");
            } else {
                setAnswer(response.data.message);
            }
        } catch (error) {
            console.error("Error fetching answer:", error);
            setAnswer("An unexpected error occurred. Please try again.");
        }
        setIsLoading(false);
    };

    const NoDocumentFound = "No Document Found";
    const aboutQF = "QueryForge is a web tool that simplifies online research by providing concise summaries of websites. By inputting a website URL, the app analyzes the content and generates clear, concise summaries that highlight the main points and arguments. This tool can be particularly useful for quickly understanding the core message of a website, saving time and effort."

    return (
        <div className="mx-5">
            <div className="mb-5">
                <h1 className="text-xl font-semibold">What is QueryForge About?</h1>
                <p className="tex-sm">{aboutQF}</p>
            </div>

            <Form className="md:flex justify-between items-center gap-5" onSubmit={handleSubmit}>
                <Input size="sm" variant="flat" className="font-semibold" radius="sm" label="Ask a question" name="question"
                    autoComplete="off"
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                />
                <div className="flex gap-4 my-5 md:my-0">
                    <Button size="md" variant="flat" className="font-bold" radius="sm" type="submit">Ask</Button>
                    <Button size="md" variant="flat" className="font-bold" radius="sm" type="button" onClick={handleIndexing}>Index the Web</Button>
                </div>
            </Form>

            <div>
                {isLoading && (
                    <div className="duration-250 ease-in-out my-7">
                        <Progress isIndeterminate size="sm" color="primary" />
                    </div>
                )}
            </div>
            
            <div className="my-5">
            {answer && (
                <div className="my-4 flex md:flex-row flex-col">
                    <div className="w-full">
                        <Markdown className="prose dark:text-white text-black">{answer}</Markdown>
                    </div>
                    <div className="w-1/3 text-sm">
                        <h1 className="text-xl font-semibold">Related Documents</h1>
                        <Accordion>
                            {Array.isArray(documents) && documents.length > 0 ? (
                                documents.map((documents) => (
                                    <AccordionItem isCompact 
                                    key={documents.metadata._id}  
                                    title={documents.metadata.source || "No source available"} 
                                    >
                                        {documents.page_content || "No content available"}
                                    </AccordionItem> 
                                ))
                            ) : (
                                <AccordionItem>{NoDocumentFound}</AccordionItem>
                            )}
                        </Accordion>
                    </div>
                </div>
            )}
            </div>
        </div>
    );
}
