from agents import CoderAgent, ReviewerAgent, FixerAgent

def run_workflow(user_requirement):
    state = {
        "requirement": user_requirement,
        "draft_code": "",
        "review_comments": "",
        "final_code": ""
    }

    print(f"🚀 开始执行 Workflow，需求：{user_requirement}")
    
    coder = CoderAgent()
    reviewer = ReviewerAgent()
    fixer = FixerAgent()

    state["draft_code"] = coder.run(state["requirement"])
    print(f"\n--- 编码完成 ---\n{state['draft_code']}")

    max_retries = 1 
    for attempt in range(max_retries + 1):
        review_input = f"原始代码：\n{state['draft_code']}"
        if state["review_comments"]:
            review_input += f"\n之前的修改说明：\n{state['review_comments']}"
            
        state["review_comments"] = reviewer.run(review_input)
        print(f"\n--- 审查结果 (尝试 {attempt+1}) ---\n{state['review_comments']}")

        if "[PASS]" in state["review_comments"]:
            print("\n✅ 代码审查通过！流程结束。")
            state["final_code"] = state["draft_code"]
            break
        else:
            print("\n🔧 发现Bug，触发修复流程...")
            fix_input = f"原始代码：\n{state['draft_code']}\n\n审查意见：\n{state['review_comments']}"
            state["final_code"] = fixer.run(fix_input)
            print(f"\n--- 修复完成 ---\n{state['final_code']}")
            state["draft_code"] = state["final_code"]

    return state

if __name__ == "__main__":
    req = input("请输入你要开发的需求（例如：写一个计算斐波那契数列的函数）：")
    final_state = run_workflow(req)
    print("\n================ 最终交付代码 ================\n")
    print(final_state["final_code"])
