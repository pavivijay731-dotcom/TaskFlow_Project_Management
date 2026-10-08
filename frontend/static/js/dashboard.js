
function showProjectForm() {
    document.getElementById("projectForm").style.display = "block";
}


function hideProjectForm() {
    document.getElementById("projectForm").style.display = "none";
}


async function loadProjects() {

    const response = await fetch("/projects/api/");
    const projects = await response.json();

    const projectList = document.getElementById("projectList");

    if (projects.length === 0) {

        projectList.innerHTML = `
            <div class="card">
                <h3>No Projects Yet 📁</h3>
                <p>Create your first project using the button above.</p>
            </div>
        `;

        return;
    }


    projectList.innerHTML = "";


    projects.forEach(function(project) {

        const card = document.createElement("div");

        card.className = "card";

        card.innerHTML = `
            <h3>📁 ${project.name}</h3>

            <p>${project.description || "No description"}</p>

            <p>
                <strong>Created by:</strong>
                ${project.created_by}
            </p>

            <p>
                <strong>Created:</strong>
                ${project.created_at}
            </p>
        `;

        projectList.appendChild(card);

    });
}


async function createProject() {

    const name =
        document.getElementById("projectName").value.trim();

    const description =
        document.getElementById("projectDescription").value.trim();

    const message =
        document.getElementById("projectMessage");


    if (!name) {

        message.textContent =
            "Please enter a project name.";

        return;
    }


    const response = await fetch("/projects/api/", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },
body: JSON.stringify({

    name: name,

    description: description

})

    });


    const data = await response.json();


    if (response.ok) {

        message.textContent =
            "Project created successfully! ✅";

        document.getElementById("projectName").value = "";

        document.getElementById("projectDescription").value = "";

        loadProjects();

    } else {

        message.textContent =
            data.error || "Something went wrong.";

    }

}


loadProjects();
