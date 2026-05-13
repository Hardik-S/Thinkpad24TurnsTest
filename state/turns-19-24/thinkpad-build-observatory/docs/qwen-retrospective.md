# Qwen Retrospective

## Direct-File Prompts Worked Best

Direct-file prompts were highly effective in our recent experiments. They allowed us to quickly iterate and test ideas without needing to parse or compile large amounts of text. This approach significantly reduced the time-to-response, making it easier for us to gather feedback and refine our models.

## Large Context Timed Out

One challenge we encountered was with handling large contexts. Our system struggled to process prompts that exceeded a certain length, leading to timeouts. We are working on optimizing our model architecture to better handle longer inputs while maintaining performance.

## Future Controllers Should Stay Tiny

In the future, we plan to focus on making our controllers as small and efficient as possible. This will help us maintain a balance between model size and inference speed, ensuring that our system remains responsive even under heavy load.

## Conclusion

Overall, our experience with Qwen has been positive, and we are excited about the potential of this technology. By focusing on direct-file prompts and optimizing our models for large contexts, we have made significant progress in improving our system's performance and user experience.
