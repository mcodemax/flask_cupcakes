// add evt listener add li to ul in form of cupcakes
//after it axios,get calls the api


//info abour CORS and troubleshooting
//https://www.youtube.com/watch?v=gPzMRoPDrFk
$cupcakeList = $('#cupcake-list')

async function makeCakeList(){
    // /api/cupcakes
    const res = await axios.get('http://localhost:5000/api/cupcakes')
    console.log(res)

    for(let cupcake of res.data.cupcakes){
        $cupcakeList.append(makeCakehtml(cupcake))
    }

}


// https://developer.mozilla.org/en-US/docs/Learn/HTML/Howto/Use_data_attributes
function makeCakehtml(cupcake){
    return `
    <div data-cupcake-id=${cupcake.id}>
      <li>
        ${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}
        <button class="del-btn">x</button>
      </li>
      <img class="Cupcake-img" src="${cupcake.image}" alt="image unavailable">
    </div>
    `;
}

$("form").on("submit", async function(evt){
    evt.preventDefault();
  
    let flavor = $("#form-flavor").val();
    let rating = $("#form-rating").val();
    let size = $("#form-size").val();
    let image = $("#form-image").val();
  
    const res = await axios.post(`http://localhost:5000/api/cupcakes`, {
      flavor,
      rating,
      size,
      image
    });
  
    let newCupcake = $(makeCakehtml(res.data.cupcake));
    $("#cupcake-list").append(newCupcake);
    $("form").trigger("reset");
  });
  

  
$("#cupcakes-list").on("click", ".del-btn", async function(evt){
    evt.preventDefault();
    let $cupcake = $(evt.target).closest("div");
    let cupcakeId = $cupcake.attr("data-cupcake-id");

    await axios.delete(`http://localhost:5000/api/cupcakes/${cupcakeId}`);
    $cupcake.remove();
    
    $cupcakeList.empty()
    makeCakeList()
});
  

$('#cupcakes-gen').on('click', async function(){
    $cupcakeList.empty()
    makeCakeList()
});