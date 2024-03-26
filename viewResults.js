import results from "./loginTestResults.json" assert { type: "json" };

const listContainer = document.getElementById('listContainer');

fillList();

function fillList(){
    results.forEach(element => {
        const node = document.createElement("div");
        node.className = "list-item";
        const nameNode = document.createElement("div");
        nameNode.append(element.username);
        nameNode.style = "font-weight: bold";
        node.appendChild(nameNode);
        const startNode = document.createElement("div");
        startNode.append("Start: " + element.test_start);
        node.appendChild(startNode);
        const endNode = document.createElement("div");
        endNode.append("End: " + element.test_end);
        node.appendChild(endNode);
        const resultNode = document.createElement("div");
        if (element.correct){
            resultNode.append("Test succeded");
            node.className += " correct-item";
            node.appendChild(resultNode);
        }
        else {
            resultNode.append("Test failed");
            const errorNode = document.createElement("div");
            errorNode.append("Error message: " + element.error_message);
            node.className += " incorrect-item";
            node.appendChild(resultNode);
            node.appendChild(errorNode);
        }
        
        listContainer.appendChild(node);
    });
  }