import React, { useEffect, useState } from 'react';
import './StoryPage.css';
import api from '../config';

function StoryPage({ storyString, streamedStory, setStreamedStory }) {
    const [title, setTitle] = useState("");
    const [storyContent, setStoryContent] = useState("");
    const [isFetched, setIsFetched] = useState(false);

    useEffect(() => {
        if (!isFetched) {
            const fetchStory = async (storyString) => {
                try {
                    setStreamedStory("");
                    setTitle("");
                    setStoryContent("");

                    const response = await fetch(`${api.API_URL}/writer`, {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                        },
                        body: JSON.stringify({
                            prompt: storyString,
                        }),
                    });

                    if (!response.ok) {
                        throw new Error("Failed to fetch story");
                    }

                    const reader = response.body.getReader();
                    const decoder = new TextDecoder();
                    let done = false;
                    let isTitleCaptured = false;

                    while (!done) {
                        const { value, done: readerDone } = await reader.read();
                        done = readerDone;
                        
                        if (value) {
                            const chunk = decoder.decode(value, { stream: true });
                    
                            if (!isTitleCaptured) {
                                const titleEndIndex = chunk.indexOf('\n\n');
                    
                                if (titleEndIndex !== -1) {
                                    setTitle(prev => prev + chunk.replace('##', ''));
                                    isTitleCaptured = true;
                                } else {
                                    setTitle(prev => prev + chunk.replace('##', ''));
                                }
                            } else {
                                setStoryContent(prev => prev + chunk);
                            }
                        }
                    }

                    setIsFetched(true);
                } catch (error) {
                    console.error("Error fetching story:", error);
                }
            };

            fetchStory(storyString);
        }
    }, [storyString, setStreamedStory, isFetched]);

    return (
        <div className="story-page">
            {title && <h2 className="story-title">{title}</h2>}
            <div className="story-content">
                {storyContent}
            </div>
        </div>
    );
}

export default StoryPage;
