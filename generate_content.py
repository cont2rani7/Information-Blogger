import google.generativeai as genai

def generate_blog_content(topic_title, gemini_api_key):
    try:
        # Configure Gemini
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel('gemini-pro')

        # Prompt to Gemini
        prompt = f"""
        Write a blog post on the trending topic: "{topic_title}".
        
        Requirements:
        - SEO-friendly title (max 60 characters)
        - Short meta description (max 155 characters)
        - Main blog content (well-formatted HTML)
        - Use bullet points, subheadings, and a quote at the end.
        - Add relevant tags and categories based on the topic.

        Respond in this format:
        Title: <your title>
        Description: <your description>
        Tags: tag1, tag2, tag3
        Category: category_name
        Content: <full HTML blog content>
        """

        response = model.generate_content(prompt)

        # Parse Gemini response
        lines = response.text.strip().split('\n')
        result = {
            'title': '',
            'description': '',
            'tags': [],
            'category': '',
            'content': ''
        }

        for line in lines:
            if line.startswith("Title:"):
                result['title'] = line.replace("Title:", "").strip()
            elif line.startswith("Description:"):
                result['description'] = line.replace("Description:", "").strip()
            elif line.startswith("Tags:"):
                result['tags'] = [tag.strip() for tag in line.replace("Tags:", "").split(',')]
            elif line.startswith("Category:"):
                result['category'] = line.replace("Category:", "").strip()
            elif line.startswith("Content:"):
                content_index = lines.index(line)
                result['content'] = "\n".join(lines[content_index + 1:])
                break
        print(f"✅ Content generated successfully for topic: {topic_title}")
        return result

    except Exception as e:
        print(f"❌ Error generating content: {e}")
        return None
