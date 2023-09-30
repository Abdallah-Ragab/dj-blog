const imageUploadInput = document.querySelector("#image-upload-input");
const imageUploadTrigger = document.querySelector("#image-upload-trigger");
const imageUploadContainer = document.querySelector("#image-upload-container");
imageUploadTrigger.addEventListener("click", () => {
  imageUploadInput.click();
});
imageUploadInput.addEventListener("change", (e) => {
  const file = e.target.files[0];
  const reader = new FileReader();
  reader.onloadend = () => {
    imageUploadContainer.style.backgroundImage = `url(${reader.result})`;
    imageUploadContainer.style.backgroundSize = `cover`;
    imageUploadContainer.style.backgroundPosition = `center`;
    imageUploadContainer.style.backgroundRepeat = `no-repeat`;
    imageUploadTrigger.classList.add("opacity-0");
  };
  reader.readAsDataURL(file);
});


$(document).ready(function () {
    $("#postContent").summernote({
      placeholder: "Write the content of your post here...",
      tabsize: 2,
      minHeight: 400,
      popover: {
        image: [
          ['image', ['resizeFull', 'resizeHalf', 'resizeQuarter', 'resizeNone']],
          ['float', ['floatLeft', 'floatRight', 'floatNone']],
          ['remove', ['removeMedia']]
        ],
        link: [
          ['link', ['linkDialogShow', 'unlink']]
        ],
        table: [
          ['add', ['addRowDown', 'addRowUp', 'addColLeft', 'addColRight']],
          ['delete', ['deleteRow', 'deleteCol', 'deleteTable']],
        ],
        air: [
          ['color', ['color']],
          ['font', ['bold', 'underline', 'clear']],
          ['para', ['ul', 'paragraph']],
          ['table', ['table']],
          ['insert', ['link', 'picture']]
        ]
      },
      toolbar: [
        ['style', ['style']],
        ['font', ['bold', 'underline', 'clear']],
        ['fontname', ['fontname']],
        ['color', ['color']],
        ['para', ['ul', 'ol', 'paragraph']],
        ['table', ['table']],
        ['insert', ['link', 'picture']],
        ['view', ['fullscreen', 'codeview', 'help']],
      ],
      callbacks: {
        onChange: function (contents, $editable) {
          document.getElementById("postContent-input").value = contents;
        },
        onImageUpload: function (files) {
          var key = "5f1262a561d418961c5cb60a0da60f71";
          var endpoint = "https://api.imgbb.com/1/upload?key=" + key;
          var image = files[0];
          const data = new FormData();
          data.append("image", image);

          console.log(image);

          fetch(endpoint, {
              method: "POST",
              body: data,
            })
            .then((response) => {
              if (response.ok) {
                return response.json();
              } else {
                throw new Error(
                  "Something went wrong with the image upload:" +
                  response.json().error
                );
              }
            })
            .then((data) => {
              $("#postContent").summernote(
                "insertImage",
                data.data.url,
                function ($image) {
                  $image.css("width", "50%");
                  $image.attr("data-filename", data.data.name);
                }
              );
            })
            .catch((error) => {
              console.error(error);
            });
        },
      },
    });
  });


  const tagHtml = (tag) => {
    return `<a data-tag-slug="${tag.slug}" data-tag-name="${tag.name}" class="px-2 py-1 bg-gray-200 dark:bg-gray-700 text-xs rounded flex items-center w-fit text-gray-600 dark:text-gray-400">
      ${tag.name}
      <button class="ml-1 font-bold text-gray-500 dark:text-gray-500" onclick=deselectTag(event)>x</button>
    </a>`;
  };
  const createTagDropdownHtml = (tag) => {
    return `<span onclick=selectTag(event) data-tag-slug="${tag.slug}" data-tag-name="${tag.name}" class="cursor-pointer block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900 dark:text-gray-400 dark:hover:text-gray-200 dark:hover:bg-gray-800">Create new tag "${tag.name}"</span>`;
  };
  const tagDropdownHtml = (tag) => {
    return `<span onclick=selectTag(event) data-tag-slug="${tag.slug}" data-tag-name="${tag.name}" class="cursor-pointer block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900 dark:text-gray-400 dark:hover:text-gray-200 dark:hover:bg-gray-800">${tag.name}</span>`;
  };
  const tagsInput = document.querySelector("input#tags-input");
  const tagsInputHidden = document.querySelector('input[name="tags"]');
  const tagsDropdown = document.querySelector("#tags-dropdown");
  const tagsList = tagsDropdown.querySelector("ul");
  const selectedTags = document.querySelector("#selected-tags");

  tagsInput.addEventListener("input", (e) => {
    console.log("input event fired");
    let value = e.target.value;
    tagsList.innerHTML = "";
    if (value.length < 1) {
      tagsDropdown.classList.add("hidden");
      return;
    }
    const url = "{% url 'blog:tag_list_json' %}" + `?search=${value}`;
    fetch(url)
      .then((res) => {
        if (res.ok) {
          return res.json();
        } else {
          console.error("Failed to fetch matching tags");
        }
      })
      .then((data) => data.tags)
      .then((tags) => {
        for (tag of tags) {
          if (tagAlreadySelected(tag)) {
            continue;
          }
          htmlElement = tagDropdownHtml(tag);
          tagsList.innerHTML += htmlElement;
        }
        htmlElement = createTagDropdownHtml({
          name: value
        });
        tagsList.innerHTML += htmlElement;
        return tags;
      })
      .then((tags) => {
        tagsDropdown.classList.remove("hidden");
      });
  });

  document.addEventListener("click", (e) => {
    if (e.target !== tagsInput) {
      tagsDropdown.classList.add("hidden");
    }
  });
  const getSelectedTagList = () => {
    tags = [];
    for (tagElement of selectedTags.children) {
      let tag = {
        name: tagElement.dataset.tagName,
        slug: tagElement.dataset.tagSlug,
      };
      tags.push(tag);
    }
    return tags;
  };

  const deselectTag = (e) => {
    const tagElement = e.target.parentElement;
    tagElement.remove();
    AddSelectedTagsToInput();
  };

  const selectTag = (e) => {
    const tagElement = e.target;
    const tag = {
      name: tagElement.dataset.tagName,
      slug: tagElement.dataset.tagSlug,
    };
    htmlElement = tagHtml(tag);
    tagsInput.value = "";
    selectedTags.innerHTML += htmlElement;
    AddSelectedTagsToInput();
  };

  const AddSelectedTagsToInput = () => {
    tags = getSelectedTagList();
    tagsInputHidden.value = JSON.stringify(tags);
  };
  const tagAlreadySelected = (tag) => {
    for (tagElement of selectedTags.children) {
      if (tagElement.dataset.tagSlug === tag.slug) {
        return true;
      }
    }
    return false;
  };