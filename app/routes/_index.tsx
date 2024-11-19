import type { MetaFunction } from "@remix-run/node";
import QuestionForm from "~/components/QuestionForm";

export const meta: MetaFunction = () => {
  return [
    { title: "Query Forge" },
    { name: "description", content: "Welcome to Query Forge!" },
  ];
};

export default function Index() {
  return (
    <div>
      <QuestionForm />
    </div>
  );
}

