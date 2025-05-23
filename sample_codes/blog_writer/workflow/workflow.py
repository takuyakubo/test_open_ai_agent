from agents import Runner, trace
from ..criteria.criteria import criteria
from ..agents.first_writer import first_writer, create_input_topic
from ..agents.reviewer import reviewer, create_input_review, get_average_score_from_, get_review_result_text_from
from ..agents.rewriter import rewriter, create_input_rewrite

async def reflection_loop(topic, N_max=5):
    w_results = []
    r_results = []
    history = []
    best_idx = -1
    best_score = 0
    base_article = ""
    review_results = ""
    
    with trace("Create Blog Content"):
        for idx in range(N_max):
            if r_results == []:
                w_input = create_input_topic(**topic)
                w_result = await Runner.run(first_writer, w_input)
            else:
                w_input = create_input_rewrite(
                    article=base_article,
                    review_results=review_results,
                    **topic
                )
                w_result = await Runner.run(rewriter, w_input)
            
            history += w_result.to_input_list()
            w_results.append(w_result)
            base_article = w_result.final_output.article_markdown
            
            r_input = create_input_review(
                article=w_result.final_output.article_markdown,
                **topic
            )
            r_result = await Runner.run(reviewer, r_input)
            history += r_result.to_input_list()
            r_results.append(r_result)

            review_data = r_result.final_output.model_dump()
            score_ = get_average_score_from_(review_data)
            if best_score < score_:
                best_score = score_
                best_idx = idx
            if score_ >= .9:
                break
            review_results = get_review_result_text_from(review_data, criteria)
    
    return list(zip(w_results, r_results)), best_idx 