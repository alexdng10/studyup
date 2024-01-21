function AddQuiz(props) {
    return (
      <li className="addquiz stack-small">
        <div className="c-cb">
          <input id={props.id} type="checkbox" defaultChecked={props.completed} />
          <label className="quiz-label" htmlFor={props.id}>
            {props.name}
          </label>
        </div>
        <div className="btn-group">
          <button type="button" className="btn">
            Complete <span className="visually-hidden"></span>
          </button>
          <button type="button" className="btn btn__danger">
            Delete <span className="visually-hidden"></span>
          </button>
        </div>
      </li>
    );
  }
  
  export default AddQuiz;
  