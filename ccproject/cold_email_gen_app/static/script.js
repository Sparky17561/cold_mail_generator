document.addEventListener("DOMContentLoaded", async function() {
    // Fetch user and client data when the page loads
    try {
        const response = await fetch('/get-user-data/');
        const data = await response.json();

        const userInfoContainer = document.getElementById('user-info-container');
        const clientDataContainer = document.getElementById('client-data-container');

        if (data.user_info) {
            // Populate the user info on the page
            userInfoContainer.innerHTML = `
                <h2>User Information</h2>
                <p><strong>Username:</strong> ${data.user_info.username}</p>
                <p><strong>Email:</strong> ${data.user_info.email}</p>
            `;

            // Check if client data exists
            if (data.client_data) {
                const clientData = data.client_data;
                clientDataContainer.innerHTML = `
                    <h2>Your Clients</h2>
                    <ul>
                        <li>
                            <strong>Name:</strong> ${clientData.name}<br>
                            <strong>City:</strong> ${clientData.city}<br>
                            <strong>2FA:</strong> ${clientData.two_fa_pass}<br>
                            <strong>LinkedIn:</strong> <a href="${clientData.linkedin}">${clientData.linkedin}</a><br>
                            <strong>Groq API Key:</strong> ${clientData.groq_api_key}<br>
                        </li>
                    </ul>
                `;
            } else {
                clientDataContainer.innerHTML = `
                    <p>No client data available.</p>
                `;
            }
        } else {
            userInfoContainer.innerHTML = `
                <p>You are not logged in.</p>
                <a href="{% url 'login' %}">Login</a>
                <a href="{% url 'register' %}">Register</a>
            `;
        }
    } catch (error) {
        console.error('Error fetching user data:', error);
    }

    // Event listener for the generate button
    document.getElementById('generate-btn').addEventListener('click', async function() {
        const jobUrl = document.getElementById('job-url').value;
        const customPrompt = document.getElementById('custom-prompt').value;

        if (!jobUrl) {
            alert("Please enter a job description URL.");
            return;
        }

        const outputField = document.getElementById('output-field');
        const scrapedJobDetailsContainer = document.getElementById('scraped-job-details'); // New container for job details
        outputField.value = "Generating email...";

        try {
            const response = await fetch('/generate-email/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ jobUrl: jobUrl, customPrompt: customPrompt })
            });

            if (response.ok) {
                const data = await response.json();
                outputField.value = data.generated_email || "No email generated.";

                // Display the scraped job details
                if (data.scraped_job) {
                    scrapedJobDetailsContainer.innerHTML = `
                        <h3>Scraped Job Details:</h3>
                        <pre>${JSON.stringify(data.scraped_job, null, 2)}</pre>
                    `;
                } else {
                    scrapedJobDetailsContainer.innerHTML = "<p>No job details scraped.</p>";
                }
            } else {
                const errorData = await response.json();
                outputField.value = "Error: " + errorData.error || "An unknown error occurred.";
            }
        } catch (error) {
            outputField.value = "Error: " + error.message;
        }
    });

    // Function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
